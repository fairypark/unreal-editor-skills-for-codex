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

Use only the source references required by the approved contract. Concept art is required when that contract names it; a floor-plan-only or functional-brief task may mark concept-art criteria `NOT_APPLICABLE` before work begins. Record the reason and approval scope. Never use `NOT_APPLICABLE` to waive a missing required reference or a failed criterion.

For the gates below, an **execution trace** means the Handbook Stage 2a record when the Handbook is available. Otherwise, create a fallback plan-feature trace recording the source and plan versions, stable feature and zone IDs, planned spatial rule and tolerance, mapped mutation scope, realized-state measurements, and pass/fail result. The fallback contract also declares the runtime camera, player height and FOV, route samples, and required checks; it does not depend on Handbook stage numbering. If design must reopen, revise and approve the responsible fallback contract or Area Composition Plan before the next affected mutation.

For a narrow operation, such as changing one Actor or checking collision, use the user's stated intent and define only the relevant postcondition. The whole-level and blockout-promotion gates below apply when that scope is actually requested.

## Clarify intent before selecting execution details

When an environment execution request leaves consequential design choices open, read [requirements-dialogue.md](references/requirements-dialogue.md) and its paired [Korean review version](references/requirements-dialogue.ko.md). Reuse the accepted brief and prior answers, explain a small set of feasible directions and a recommendation, and ask only about unresolved choices that change the current work. Feed the answers into the existing Handbook or fallback contract before selecting tools and parameters. A clear narrow operation needs only its relevant postcondition; do not restart concept discovery or infer approval from silence.

## Load only execution guidance

- Read [editor-environment-operations.md](references/editor-environment-operations.md) for Landscape, terrain, water, materials, PCG, Foliage, transforms, collision, or batch changes.
- Read [evidence-and-supervision.md](references/evidence-and-supervision.md) when capturing fixed-camera evidence or handing artifacts to an independent reviewer.
- Read [production-asset-operations.md](references/production-asset-operations.md) when installing, adapting, or packaging the bundled dependency-free production contracts.
- Read [vegetation-and-ground-cover.md](references/vegetation-and-ground-cover.md) for vegetation source failures or coupled substrate/placement fields, and [capture-fallback.md](references/capture-fallback.md) only for a documented capture exception. Their paired [Korean review](references/environment-reuse-review.ko.md) preserves the decision boundaries.
- Read [visual-quality-onboarding.md](references/visual-quality-onboarding.md) only when creating or integrating a project-owned visual-quality workspace.

## Mandatory Area Composition Plan preflight

For every new level, broad rebuild, or map-wide layout correction, place a blocking **Area Composition Plan** gate after the approved source references and before the first cube or graybox prototype:

1. Locate the versioned plan artifact and its workflow record. Verify the applicable source references, plan ID or path, version, status, reviewer or approver, and rollback target. Use the predeclared concept-art applicability from the contract.
2. Verify that the plan depicts zone boundaries and stable IDs, terrain elevations and steps, primary circulation, rivers and bridges, building footprints and typology hierarchy, and fixed validation cameras where applicable. Record a reasoned `NOT_APPLICABLE` for absent systems before work; do not omit required fields silently.
3. Keep the gate `PENDING_EVIDENCE` or `FAIL` when the artifact or record is missing, retrospective, incomplete, or unapproved. Do not create the first cube, terrain blockout, architecture proxy, or broad asset-placement batch until the gate is `PASS`.
4. For a typology-critical precinct, verify the required sequence, hierarchy, negative space, and prohibited silhouette. A palace must show the gate -> outer court -> middle gate -> central courtyard -> main hall axis and courtyard hierarchy; matching building sizes alone does not pass, and a fortress- or castle-like silhouette is a hard failure.
5. Reopen the gate when later terrain, route, water, footprint, typology, or camera changes invalidate the recorded plan. Preserve the accepted predecessor and failed candidate.

This preflight is mandatory even for small or disposable work. The plan may be lightweight, but it must exist and be recorded before geometry mutation rather than reconstructed from a blockout afterward.

## Enforce the approved floor plan during blockout

When the approved Area Composition Plan includes a floor plan, its exact approved version becomes the spatial mutation lock for the playable skeleton, representative slice, and full blockout. Do not treat it as optional visual guidance.

1. Before the first content-bearing mutation, load the plan version, coordinate frame, origin, axes, units and scale, stable plan feature and zone IDs, planned bounds or anchors, orientations, route centerlines and widths, terrain height bands, water and crossings, required negative spaces, spatial relationships, and tolerances. Keep geometry read-only when any value needed to test the requested placement is missing, stale, unresolved, or unapproved.
2. Before every mutation batch, map each requested Actor, component, spline, terrain change, or deterministic group to its plan feature ID, zone ID, execution trace entry, planned spatial rule, and allowed deviation. Reject unmapped or freehand placement even when it is called temporary or exploratory.
3. Execute only the mapped bounded batch, then re-query the realized transforms, bounds, footprints, entrances and orientations, spline points and widths, surface elevations, zone containment, required-void occupancy, and other declared relationships. Compare them to the same approved plan version; Actor count and tool success are not conformance evidence.
4. Mark the batch `FAIL`, preserve the last accepted baseline and failed candidate, set the placement lock closed, and stop all subsequent blockout placement when any result is unmapped, in the wrong zone, or outside tolerance. Repair or revert to the approved plan before continuing.
5. When playtest or implementation evidence requires a different layout, reopen the Area Composition Plan and its execution trace gates, approve a new plan version, and regenerate affected traces and checks before the next mutation. Do not backfit the plan to legitimize geometry already placed.

## Gate blockout promotion through independent supervision

Before a completed playable blockout advances to a representative visual slice, full layout, production meshing, or dressing, require `BLOCKOUT_REFERENCE_FIDELITY_REVIEW=PASS` from a separate read-only independent supervisor. Follow host or project policy for reviewer configuration and keep the builder unable to approve its own work.

1. Build a neutral supervisor packet from the exact applicable approved source-reference and floor-plan versions, execution trace and conformance records, fixed overview captures, the runtime-camera captures or route samples declared by the current contract, applicable rubric and hard failures, previous comparable packet, and factual change scope. Verify evidence integrity immediately before handoff and never include a desired verdict, builder score, implementation defense, or completion claim.
2. Require the supervisor to evaluate concept massing, silhouette, hierarchy, depth, reveal, negative space, and prohibited readings; floor-plan zones, footprints, orientations, routes, height bands, crossings, voids, sequence, and tolerances; and runtime-camera traversal, enclosure, pacing, readability, recovery, and POI flow. Evaluate only categories required by the approved source contract; retain its predeclared `NOT_APPLICABLE` decisions. A pass requires every applicable category to meet the predeclared floor and no hard failure.
3. On `FAIL`, record the evidence-grounded defects, weakest system, regressions, and one bounded next change. Repair one major system, recapture the same cameras and runtime samples, create a new immutable packet, and invoke a fresh independent review. Repeat until the exact candidate receives `PASS`; self-review cannot promote the blockout.
4. When materially distinct repairs repeatedly fail or show no credible improvement, stop broad mutation and record a root-cause analysis. Separate implementation, asset, terrain or route representation, tool, capture, evaluator, platform, and budget causes from contradictory, underspecified, or infeasible concept-art or floor-plan requirements. Record `DESIGN_REVIEW_REQUIRED` and reopen the responsible Handbook Stage 1, Stage 2, or Stage 2a when available, or the responsible fallback contract, Area Composition Plan, and execution trace otherwise, before further placement when source redesign may be needed; do not weaken the rubric or backfit the plan.
5. Record an iteration/time budget and expected capture/review latency before the loop. Report any material delay to the user immediately when discovered, including supervisor unavailability, timeout or unstable Editor state, invalid evidence, broken camera comparability, reference conflict, missing asset or representation capability, repeated no-improvement, or projected budget overrun. State cause, impact, gate and lock state, elapsed time and attempts, safe work that can continue, recovery options, and any decision needed. Do not wait for the budget to expire and do not interpret the report as permission to skip the gate.

## Retire blockout cubes from the production visual surface

Before production work in a representative slice, declare its candidate boundary and inventory every blockout cube and primitive that can contribute to its required views or runtime states. Assign exactly one disposition: `REPLACE`, `RETIRE`, or `RETAIN_INTERNAL_SKELETON`. After the independent fidelity gate passes, bounded replacement and meshing within that scope are permitted to satisfy this retirement gate; retirement `PASS` is required for slice acceptance and promotion, not to begin the replacement itself. Unfinished blockout outside the candidate boundary may remain only when it cannot contribute to that candidate's acceptance evidence. Repeat the gate for each expanded production scope and cover the entire requested level before full-level acceptance.

1. Record the stable Actor or component identity, zone and plan feature, execution trace entry, current material, visibility, collision, support or navigation responsibility, and intended production disposition. Do not infer retirement from a renamed folder or hidden Outliner row.
2. For `REPLACE`, transfer the approved spatial and trace contract to the production visual asset or authored system before removing or disabling the proxy. For `RETIRE`, prove that no required collision, support, navigation, measurement, or traceability duty remains.
3. Permit `RETAIN_INTERNAL_SKELETON` only when the cube remains a non-visual internal skeleton or has an explicit support or collision duty. Keep it fully enclosed or non-rendering in every declared runtime state. Do not expose a face, assign a production finish material, use it as a decal-bearing surface, or present a materialized blockout cube as production art.
4. Verify runtime-camera, fixed-overview, reverse, contact, streaming, LOD or HLOD, visibility, occlusion, and variant states. Fail on exposed corners, gaps, seams, z-fighting, shadows, reflections, or silhouette contribution from retained skeletons.
5. Record `BLOCKOUT_CUBE_VISUAL_RETIREMENT=PASS` only for the exact verified candidate. Any visible or material-finished blockout primitive contributing to the declared production candidate blocks its acceptance and expansion even when the independent reference-fidelity review passed. Keep bounded replacement and repair available; do not turn this check into a prerequisite for the work needed to pass it.

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

## Gate blank-level observation lighting behind approved design

Treat lighting, sky, atmosphere, fog, exposure, and post-process setup in a
newly created blank level as implementation mutation. The blank level may be
created, saved, and inspected read-only earlier, but do not spawn or modify
those Actors while the concept or floor-plan design remains unresolved.

Before the first such lighting mutation, verify the design handoff:

1. When the Handbook is available, require `PASS` for Stage 1 Concept and
   Intent, Stage 2 Area Composition Plan, Stage 2a translation, and the
   applicable Stage 2b asset-plan decision.
2. When the Handbook is unavailable, require the approved minimum fallback
   contract and Area Composition Plan before adding the observation setup.

Keep the lighting mutation read-only while any required design artifact is
missing, changed, `PENDING_EVIDENCE`, `INVALID_EVIDENCE`, or `FAIL`. Only after
the design prerequisites pass, and before the first primitive, terrain, route,
architecture, or dressing mutation:

1. Verify the intended saved world, record and preserve its World Partition
   mode under the approved project contract, and inventory existing lighting,
   atmosphere, fog, exposure, and post-process state. Do not change partition
   mode merely to establish observation lighting.
2. If the level has no intentional authored observation environment, create the
   smallest shared baseline that makes scale, silhouettes, contacts, seams,
   depth, and open-versus-closed boundaries readable. Use a key light, ambient
   or sky contribution, locked exposure, and only restrained atmosphere, fog,
   or local fill when those are necessary for diagnosis.
3. Record the exact baseline in the level's Visual Recipe or workflow record.
   Do not hard-code project-independent lighting numbers in this Skill.
4. Place or identify the approved human-scale reference and inspect one
   player-height diagnostic frame. Geometry remains read-only if the frame is
   washed out, clipped, crushed into black, or otherwise cannot reveal floor,
   wall, ceiling, depth, contact, and enclosure state.
5. Freeze the baseline across comparison variants. Any local diagnostic fill
   must be symmetric, recorded, and unable to hide gaps, leaks, or exposed
   proxy geometry.

Do not replace an existing intentional lighting design, a lighting-neutral
structural-audit contract, or an explicitly approved dark or unlit target.
Preserve that state and record the exception instead. When the approved target
is intentionally dark or unlit, perform structural diagnosis in a separate,
clearly labeled `DIAGNOSTIC_ONLY` observation pass; never use that pass as beauty
or release approval evidence. Actor creation alone does not pass this gate:
re-read the resulting properties and inspect the diagnostic frame before
geometry work begins.

## Execute in bounded stages

### 0. Area Composition Plan and design preflight

- Record the applicable source-reference artifacts, versions, status, and approver, then record the plan artifact, version, status, source-reference lineage, required fields, fixed-camera contract, and gate result. Carry predeclared `NOT_APPLICABLE` decisions without treating absent required evidence as optional.
- When the Handbook is available, also record the Stage 2a translation and applicable Stage 2b asset-plan decisions. Otherwise record the fallback plan-feature trace and declared runtime evidence contract.
- When the plan includes a floor plan, record its spatial-lock coordinate frame, stable feature IDs, tolerances, and the exact version that every blockout batch must implement.
- Stop lighting setup, geometry, and broad placement mutation unless this design preflight is `PASS`; do not infer a concept or plan from implementation state.

### 0a. Post-design blank-level observation baseline

- Only after the design preflight passes, install or preserve the observation baseline in a newly created blank level and pass its gate before the first geometry mutation.
- Store the verified baseline state, scale-reference identity, diagnostic camera, exception status, and A/B freeze status with the workflow evidence.
- If geometry was created first, do not silently backfill the gate. Mark that stage invalid, establish the baseline, and repeat the affected stage or explicitly bound it out of the result.

### 1. Playable skeleton

- After the design preflight passes, create or verify the complete zone-marker set, pass the post-design blank-level observation-baseline gate, and only then create or modify terrain, primary circulation, PlayerStart, boundaries, water, and traversal transitions. Bind every content-bearing change to its approved floor-plan feature and pass the post-batch spatial-conformance audit before the next batch.
- Measure representative surface heights, route widths, slopes, steps, and capsule clearance.
- Save, re-read changed state, and run a short PIE traversal before dressing.

### 1a. Independent blockout reference-fidelity gate

- Freeze the candidate version, verify the complete applicable source/plan/overview/runtime evidence packet, and submit it to the separate read-only supervisor.
- Keep Stage 2, full layout, production meshing, and dressing locked on `FAIL`, `PENDING_EVIDENCE`, or `INVALID_EVIDENCE`.
- On failure, repair the named weakest system and repeat same-condition capture and independent review. On non-convergence, run root-cause analysis and reopen design with `DESIGN_REVIEW_REQUIRED` when warranted.
- Report any material delay immediately; silent retries and builder self-approval are gate failures.

### 1b. Blockout-cube visual-retirement gate

- Declare the bounded slice candidate and inventory every blockout cube and primitive that can contribute to its acceptance views or runtime states. Bind each to the approved plan and execution trace record, and assign `REPLACE`, `RETIRE`, or `RETAIN_INTERNAL_SKELETON`. Repeat for each later expansion.
- Keep a retained internal skeleton fully enclosed or non-rendering and preserve only its explicitly recorded structural, support, collision, navigation, or traceability duty. Material assignment never promotes blockout geometry to a production visual surface.
- Inspect the exact candidate from runtime, fixed overview, reverse, contact, streaming, LOD or HLOD, visibility, and variant conditions. Record a hard failure for any exposed face, production-finish material, seam, z-fighting, shadow, reflection, or silhouette contribution.
- Permit bounded replacement and meshing after Stage 1a passes. Keep slice acceptance and expansion locked until `BLOCKOUT_CUBE_VISUAL_RETIREMENT=PASS` is recorded for the exact candidate; do not require whole-level retirement before making the first slice.

### 2. Representative slice

- After Stage 1a records `BLOCKOUT_REFERENCE_FIDELITY_REVIEW=PASS` and Stage 1b records the bounded disposition plan, implement one bounded segment that exercises the selected terrain, route, architecture or focal prop, contact treatment, materials, vegetation, lighting, collision, and reverse view. Complete its replacements and verify `BLOCKOUT_CUBE_VISUAL_RETIREMENT=PASS` before accepting the slice or expanding its systems.
- Keep the active zone marker readable in local evidence and all zone markers readable in overview or arrival evidence.
- If the slice contains architecture, pass the `$building-grounding` four-corner gate before duplicating its placement pattern.
- Capture the agreed fixed views and run the required functional, visual, and performance checks.
- Do not duplicate the system across the level until the slice satisfies the design contract.

### 3. Full layout and dressing

- Scale the verified systems with deterministic seeds and explicit exclusions where procedural generation is used. Repeat the disposition inventory and visual-retirement checks for every expanded production scope; a slice pass does not approve remaining blockout elsewhere. Require full requested-level coverage before full-level acceptance.
- Preserve every `RETAIN_INTERNAL_SKELETON` record as non-visual through proxy replacement, dressing, streaming, and LOD or HLOD changes; never expose or production-material-finish the retained cube during a later batch.
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

For the mandatory blockout reference-fidelity gate, keep the reviewer read-only and separate from the builder. Give it raw references, verified captures, the applicable project rubric, and factual change scope. Follow the host or project policy for reviewer model and reasoning settings. When no independent reviewer is available, label any diagnostic pass `self-review; not independently supervised`, keep promotion `PENDING_EVIDENCE`, and report the delay immediately; self-review cannot satisfy this gate.

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

The requested live Editor state matches the approved brief and relevant postconditions. For new-level, broad-layout, or blockout-promotion work, the applicable source references and versioned Area Composition Plan passed before blank-level lighting, geometry, or broad placement mutation. The exact approved plan remained the spatial mutation lock, and each content-bearing batch passed execution-trace mapping and realized spatial-conformance checks. The Handbook or fallback trace and runtime-evidence contract remained usable throughout.

Before production work, a separate read-only supervisor issued `BLOCKOUT_REFERENCE_FIDELITY_REVIEW=PASS` for the exact applicable references, plan, blockout, camera, and evidence versions. Failed reviews received bounded repair and comparable recapture; non-convergence received root-cause and possible `DESIGN_REVIEW_REQUIRED` handling, and material delays were reported immediately. Every primitive contributing to an accepted production scope has a recorded disposition and `BLOCKOUT_CUBE_VISUAL_RETIREMENT=PASS`; this is verified after bounded replacement and before accepting or expanding the slice, and across the entire requested level before full-level acceptance. Retained internal skeletons remain non-visual in every declared state.

Each new blank level passed a readable post-design observation baseline before its first geometry mutation and kept it frozen across compared variants, preserving approved partition mode and intentional dark-state exceptions. Applicable typology rules, player-camera views, zone-marker lifecycle, and the `$building-grounding` four-corner gate or explicitly approved foundation/grade exception passed. Overview captures remain diagnostic-only. Traversal, collision, navigation, streaming, performance, warnings, and saved state meet the task's contract. Report failed or pending evidence truthfully; successful MCP execution alone never implies design or release approval.
