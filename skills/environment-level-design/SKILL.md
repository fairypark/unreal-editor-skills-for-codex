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
3. If the Handbook plugin is not installed, do not block the task. Record a minimum fallback contract: intended player experience, playable envelope, route and focal point, allowed assets, platform or performance constraints, recovery point, required views, runtime checks, and definition of done.
4. Do not reproduce Handbook chapters inside project notes or this Skill. Preserve only project-specific decisions and evidence.

For a narrow operation, such as changing one Actor or checking collision, use the user's stated intent and define only the relevant postcondition.

## Load only execution guidance

- Read [editor-environment-operations.md](references/editor-environment-operations.md) for Landscape, terrain, water, materials, PCG, Foliage, transforms, collision, or batch changes.
- Read [evidence-and-supervision.md](references/evidence-and-supervision.md) when capturing fixed-camera evidence or handing artifacts to an independent reviewer.
- Read [production-asset-operations.md](references/production-asset-operations.md) when installing, adapting, or packaging the bundled dependency-free production contracts.
- Read [visual-quality-onboarding.md](references/visual-quality-onboarding.md) only when creating or integrating a project-owned visual-quality workspace.

## Inspect before mutation

1. Read applicable project instructions and registered Unreal Agent Skills.
2. Confirm the target `.uproject`, open world, current selection, and intended construction provenance.
3. Create or confirm a source-control or saved-copy recovery point before broad mutation.
4. Discover only the Unreal toolsets required for the next stage. Keep game-thread MCP calls sequential.
5. Prefer structured Unreal tools. Use UI control only for the smallest unavoidable action and stop controlling it immediately afterward.
6. Inspect source assets at final scale before map-wide use. Check class, bounds, pivot, material slots, collision intent, LOD or Nanite behavior, and dependencies.

## Execute in bounded stages

### 1. Playable skeleton

- Create or modify terrain, primary circulation, PlayerStart, boundaries, water, and traversal transitions.
- Measure representative surface heights, route widths, slopes, steps, and capsule clearance.
- Save, re-read changed state, and run a short PIE traversal before dressing.

### 2. Representative slice

- Implement one bounded segment that exercises the selected terrain, route, architecture or focal prop, contact treatment, materials, vegetation, lighting, collision, and reverse view.
- Capture the agreed fixed views and run the required functional, visual, and performance checks.
- Do not duplicate the system across the level until the slice satisfies the design contract.

### 3. Full layout and dressing

- Scale the verified systems with deterministic seeds and explicit exclusions where procedural generation is used.
- Re-read representative Actors or generated components after each batch.
- Finish reachable reverse views, boundaries, contacts, and secondary routes rather than optimizing only the hero camera.
- Save affected levels and owned assets after successful stage checks.

### 4. Integration and polish

- Verify Landscape layers, material scale, lighting state, streaming, LOD or instancing, collision, navigation, warnings, and persistence.
- Change one major system per comparison pass and recapture the same cameras.
- If a tool call times out, inspect the resulting state before retrying to avoid duplicate Actors or repeated generation.

## Capture and review evidence

Use persistent `CameraActor` evidence for required arrival, focal, route, reverse, elevated, and contact views. When `VisualEvidenceExtensionToolset` is available, use `CaptureCameraToPng`, retain its paired receipt and returned trust anchors, then call `VerifyEvidenceForSupervision` immediately before handoff.

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

The requested live Editor state matches the approved brief; required postconditions and representative views are verified; traversal, collision, navigation, streaming, performance, and warnings meet the task's contract; saves persisted; failed or pending evidence is reported truthfully; and no design approval is inferred merely from successful MCP execution.
