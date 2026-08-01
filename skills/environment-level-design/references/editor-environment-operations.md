# Editor Environment Operations

Use this reference only for live Unreal Editor execution. Obtain the spatial and production design contract from `design-unreal-worlds-and-levels` when the Handbook plugin is installed, or from the minimum fallback contract in the parent Skill.

## Landscape and terrain

- Inspect the open world, World Partition state, Landscape layout, physical dimensions, component settings, XY and Z scale, materials, and collision before changing them.
- Resolve a trusted terrain surface before ground placement. A trace that hits a prop, volume, or generated instance is not terrain evidence.
- Modify macro terrain and routes before dense dressing. After changes, sample representative surface positions and normals, then verify traversal in PIE.
- Grade building footprints or create explicit foundations. Check the center, corners, and edge midpoints rather than relying on one center trace.
- Re-read Landscape and affected Actor state after a batch, then save the owned level and assets.

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

At each stage, record the changed systems, affected objects or assets, saves, warnings, runtime checks, evidence paths, and unresolved blockers. A stage remains pending when required live checks or evidence have not run.
