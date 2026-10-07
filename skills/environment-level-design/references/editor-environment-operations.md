# Editor Environment Operations

Use this reference only for live Unreal Editor execution. Obtain the spatial and production design contract from `design-unreal-worlds-and-levels` when the Handbook plugin is installed, or from the minimum fallback contract in the parent Skill.

## Area Composition Plan preflight

- Resolve the plan artifact and workflow record before discovering mutation tools. Record plan ID or path, version, source concept, status, reviewer or approver, and rollback target.
- Validate zone boundaries and stable IDs, terrain elevations and steps, primary circulation, rivers and bridges, building footprints and typology hierarchy, and fixed validation cameras. Treat each as a required field, not optional illustration detail.
- When the plan is missing, incomplete, retrospective, or not `PASS`, perform read-only inspection only. Do not create cube or graybox geometry, terrain blockout, architecture proxies, or broad asset batches.
- Recheck affected plan entries before a batch that changes terrain height, route topology, water crossings, building footprints, typology, or fixed cameras. Reopen the plan gate rather than silently diverging.

## Landscape and terrain

- Inspect the open world, World Partition state, Landscape layout, physical dimensions, component settings, XY and Z scale, materials, and collision before changing them.
- Resolve a trusted terrain surface before ground placement. A trace that hits a prop, volume, or generated instance is not terrain evidence.
- Modify macro terrain and routes before dense dressing. After changes, sample representative surface positions and normals, then verify traversal in PIE.
- Grade building footprints or create explicit foundations. Check the center, corners, and edge midpoints rather than relying on one center trace.
- Re-read Landscape and affected Actor state after a batch, then save the owned level and assets.

## Zone markers and scale evidence

- Resolve a stable zone registry before prototype geometry: stable ID, numeric review ID, display name, ASCII fallback, role, anchor or bounds, semantic color, and marker owner.
- Place one editor/debug marker per zone in a dedicated folder or Data Layer with a consistent tag such as `LD_ZONE_MARKER`. Make every label include the numeric ID plus ASCII fallback, such as `03 PALACE PRECINCT`; keep localized text additive and never depend on the active font supporting it. Treat empty glyphs or clipped fallback text as a failed marker. Keep production geometry and runtime signage separate from this contract.
- After broad deletes, resets, proxy replacement, PCG generation, or asset-placement batches, compare the complete marker inventory by ID, label, transform or bounds, visibility, folder or layer, and tag.
- Keep markers visible from the first prototype mutation through completed production asset placement. Retire them only in an explicit recorded cleanup after overview, local, reverse-view, and inventory evidence pass.
- Capture overall views with every zone name readable. Capture local building-scale views with the active zone name and an agreed player-scale character or metric reference visible together.

## Typology-critical layout checks

- Translate the approved footprint, orientation, axis, courtyard or street hierarchy, negative space, and prohibited silhouette directly from the Area Composition Plan before placing architecture proxies.
- Do not approve a typology from width, length, height, or Actor bounds alone. Test the sequence from the gameplay approach and reverse views.
- For a palace, verify the gate -> outer court -> middle gate -> central courtyard -> main hall axis and the hierarchy of open courts and supporting halls. Record a hard failure if the result reads as a fortress or castle through a dominant keep, tower-like blocks, monolithic plinth, or continuous high defensive wall.
- On typology failure, stop architecture duplication and broad dressing, preserve the failed candidate, and return to the Area Composition Plan.

## Materials, water, and lighting

- Inspect current material assignments, layer info, parameter ownership, texture scale, and shader state before replacement.
- Apply Landscape or water changes to a bounded test area first. Verify layer coverage, seams, banks, translucency, reflections, and collision intent.
- Change one major lighting or atmosphere variable at a time. Compare the same persistent cameras after temporal rendering settles.
- Treat shader compilation, streaming, or asset compilation as pending state. Do not capture acceptance evidence until they complete.

## PCG, Foliage, and repeated systems

- Inspect source meshes with their final materials and intended scale ranges before graph or Foliage setup.
- Give each generator one responsibility and explicit path, building, water, sightline, and gameplay exclusions.
- Prefer deterministic seeds for comparisons. Expose one candidate generation at a time and disable superseded components before capture.
- After generation, record component or instance counts by responsibility, warnings, regeneration time, collision and overlap behavior, Navigation influence, coverage, and representative grounding checks.
- Before the first mutation for dependent strata such as rocks or hardscape plus grass or ground cover, verify the workflow record contains a `Dependent-Strata Strategy Gate` with `CONSIDERED`, a selected mode (`VIDEO_DISTANCE_EXCLUSION`, `MASK_OTHER`, `DIRECT_AUTHORED`, or `PENDING_EVIDENCE`), the decision reason, source authority, dependency order, units, clearance, transition band, and validation status. If the applicable gate is missing or pending, keep the dependent placement read-only.
- When `VIDEO_DISTANCE_EXCLUSION` is selected for ground cover around generated hardscape, use the hardscape output or a recorded conservative footprint as the single exclusion authority. Record the clearance or transition band and validate the final bounds gap; do not rely only on center-point distance.
- Do not infer that enabling Nanite enables distance culling. Record the engine and target platform, then verify the actual visibility, streaming, popping, frame-time, and memory behavior before accepting an optimization setting.
- For multi-part clusters, preserve parent-child transforms through filtering and variation. Removing a required parent must also remove dependent children.
- Sample broad footprints at the center and surrounding points. A center hit or bounding box alone does not prove contact.
- Runtime diagnostics do not approve visual quality; submit fixed-camera evidence separately.

## Collision and navigation

1. Identify the exact defect: preset, response, simple collision, complex collision, transform, capsule pinch point, physics, or Navigation mismatch.
2. Preserve a visually appropriate placement while testing the narrowest safe correction.
3. Use project-local variants when changing a shared source asset would affect other levels.
4. Retest with the actual player capsule at ankle, torso, and head contact heights and from both traversal directions.
5. Verify entrances, steps, banks, bridge ends, roots, narrow gaps, camera movement, physics, and Navigation.
6. Delete or replace an asset only when it is itself unsuitable and the requested design scope permits that change.

## Transform and batch safety

- Read complete transforms before mutation and preserve location, rotation, and scale together.
- Keep Unreal game-thread calls sequential.
- Use small batches with explicit targets and postconditions.
- Re-query representative objects after each batch.
- If a call times out, inspect the resulting state before retrying.
- Actor count detects missing or duplicate batches; it is not evidence of spatial or visual quality.

## Stage verification

At each stage, record the Area Composition Plan ID and version, changed systems, affected objects or assets, zone-marker inventory, saves, warnings, runtime checks, evidence paths, and unresolved blockers. A stage remains pending when required live checks or evidence have not run.
