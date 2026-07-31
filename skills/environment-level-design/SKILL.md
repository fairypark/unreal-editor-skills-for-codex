---
name: environment-level-design
description: Set up, design, build, rebuild, dress, or review production-quality Unreal Engine environment levels from concept through Landscape, architecture, vegetation, materials, lighting, gameplay, collision, and 360-degree visual QA. Use for new Unreal project environment workflows, new outdoor maps, open-world spaces, culturally specific environments, terrain-led level design, environment quality recovery, golden slices, independent visual supervision, or reusable level-design standards. Do not use for a single isolated Actor placement or purely conceptual questions with no level work.
---

# Environment Level Design

Build an environment as a playable place, not a camera-facing diorama. Treat every stage as a quality gate: stop scaling when topology, assets, contact, or representative views do not yet meet the chosen reference.

## Load only the guidance the task needs

- Read [quality-gates.md](references/quality-gates.md) for every build or review.
- Read [visual-first-production-legacy.md](references/visual-first-production-legacy.md) for every build, rebuild, or review so new work inherits proven visual-first decisions without copying project-specific values.
- Read [reusable-production-assets.md](references/reusable-production-assets.md) when preserving, promoting, packaging, installing, or reusing production assets across levels, projects, teams, or users.
- Read [independent-visual-supervision.md](references/independent-visual-supervision.md) for every multi-system level build, rebuild, dressing pass, visual-quality recovery, golden slice, or full-level acceptance review.
- Read [visual-quality-onboarding.md](references/visual-quality-onboarding.md) when setting up a new Unreal project, when no project-owned visual policy exists, or when the user asks about Visual Recipes or quality-gate adoption.
- Read [codex-mini-arena-case-study.md](references/codex-mini-arena-case-study.md) only when an onboarding decision benefits from a compact worked example. Treat it as a procedural case study, never as a preset.
- Also read [landscape-ecology-and-collision.md](references/landscape-ecology-and-collision.md) when the level contains outdoor terrain, water, vegetation, Landscape materials, PCG, Foliage, or placed mesh collision.
- Use [level-brief-and-iteration-log.md](references/level-brief-and-iteration-log.md) when starting a level, rebuilding a failed one, or preserving lessons for later maps.

## Establish authority and provenance

1. Read relevant project-registered Unreal Agent Skills and any active project-owned production legacy when a live project exposes them. Treat this Codex skill as the reusable baseline and project skills as narrow overrides or additions. Inherit gates and decision patterns; revalidate map-specific assets, transforms, densities, light values, and procedural parameters in the new concept.
2. Inspect the live Editor and discover only the toolsets needed for the next stage. Do not preload or restate every tool schema.
3. Prefer structured Unreal tools over screen control. If UI control is unavoidable, use it for the smallest possible action and stop observing or controlling the UI immediately afterward.
4. Declare one construction mode:
   - **Blank-level concept-led:** create an original layout without duplicating or sampling an existing authored map.
   - **Source-assisted:** reuse a level only when the user authorizes it and the source genuinely fits the route, enclosure, collision, and visual goals.
5. Reuse approved individual assets in either mode. Never switch provenance silently because an existing level is convenient.

## Offer project-owned visual quality setup

When a new project or environment task has no project-owned visual policy:

1. Inspect `AGENTS.md`, registered project skills, and existing `Docs/VisualQuality` files before proposing anything.
2. Briefly introduce the optional Visual Recipe and independent-supervision workflow. Mention the CodexMiniArena case study as an example of the procedure and judgment structure, not as a configuration to copy.
3. Let the project select `off`, `recommended`, or `strict`. Default to `recommended` only when no higher-priority instruction chooses another mode.
4. Adapt the templates under `assets/visual-quality/` to the project's genre, scale, team, performance target, and evidence needs. Do not silently write or overwrite `AGENTS.md`.
5. Keep project-specific categories, thresholds, camera roles, hard failures, asset rules, and stage requirements in project-owned files. The reusable skill supplies the workflow, not universal art direction.
6. Never let a level recipe weaken a required project threshold. User instructions and project policy remain authoritative.

## Create a decision-ready visual brief

Before layout, turn the request into observable targets.

1. If the user has not supplied a decisive visual direction, generate two to four concept variants and select one primary concept with the user or by clearly stated best judgment.
2. Include at least an arrival view, hero view, route view, and reverse view across the concepts or supporting sketches. A single facade view is insufficient.
3. Record:
   - setting, era, biome, weather, time, and emotional tone;
   - playable envelope, expected route length, expansion directions, and performance target;
   - macro terrain silhouette and height-band roles;
   - focal hierarchy, reveal order, loops, boundaries, and sightlines;
   - architecture, vegetation strata, material palette, water behavior, and atmosphere;
   - required asset families and prohibited motifs;
   - the selected quality reference and the evidence required to match it.
4. Convert the concept into a zone-to-asset coverage matrix. “Use many assets” means every asset family receives a coherent spatial or narrative role, not indiscriminate scattering.
5. When the project adopts the workflow, preserve these decisions in its Visual Recipe rather than relying on chat history or the current viewport.

## Pass asset readiness before map-scale production

1. Inspect the assets already available to the user. Use an owned-asset catalog when one is available; otherwise inspect project content.
2. Build a lineup at final scale for terrain pieces, architecture, walls, canopy, understory, ground cover, rocks, water edges, and focal props.
3. Judge cultural and biome fit from appearance rather than filenames.
4. Check mesh scale, pivots, material compatibility, LOD or Nanite behavior, collision intent, and back-side quality.
5. Stop or reduce scope if the available set cannot support the selected reference without obvious primitives, extreme scaling, or repetition.

## Start independent visual supervision

When agent delegation is available, assign one separate read-only visual supervisor before expanding the golden slice. Keep the primary agent as the builder and reuse the same supervisor for focused target reviews and full-level acceptance.

Spawn the supervisor with `model="gpt-5.6-sol"` and
`reasoning_effort="xhigh"` when supported. Prefer a project- or user-defined
`visual_critic` role. If those settings are unavailable, use the highest
supported reasoning effort, disclose the fallback, and keep the supervisor
read-only.

Give the supervisor raw concepts, fixed-camera captures, the rubric, and only the factual change scope. Do not leak the intended verdict or the builder's self-assessment. A supervisor target `PASS` does not imply full-level `GO`, and an unresolved supervisor hard failure blocks completion.

When delegation is unavailable, run the same review as a separate pass and label it `self-review; not independently supervised`. Do not claim that an independent gate occurred.

## Build in gated passes

### 1. Terrain and gameplay skeleton

- Build coherent macro terrain before architecture and dressing.
- Define low ground, primary circulation ground, and at least one elevated terrace, ridge, bank, or overlook.
- Reserve a larger coherent Landscape envelope for plausible future expansion while keeping the current playable area focused.
- Grade local building pads or author deliberate foundations before placing structures.
- Establish PlayerStart, primary route, optional loops, reveals, boundaries, water, and traversal transitions.
- Prove terrain surface heights, slopes, route clearance, and reachable height bands with measurements and player-height views.

Do not proceed if the whole playable land reads as one plane, if architecture is being used to fake terrain relief, or if the route is not traversable.

### 2. Golden slice

Finish one representative 10-30 m gameplay segment before scaling:

- final terrain transition and route;
- one focal structure or prop;
- believable architecture-to-ground and water-to-bank contact;
- layered vegetation and intentional negative space;
- final materials, lighting direction, boundary treatment, and reverse view.

Compare it with the primary concept from fixed player-height and elevated cameras. Expand only after it passes every applicable quality gate.

### 3. Full layout and ecology

- Scale the validated systems, not merely the Actor count.
- Maintain route readability, focal hierarchy, and local variation.
- Use procedural systems for repeatable spatial logic and hand placement for hero composition, transitions, and story detail.
- Finish every playable direction, including backs of buildings, secondary courts, arrival boundaries, and views away from the hero camera.
- Preserve intentional open space; define it with terrain edges, material transitions, landmarks, and sightlines rather than filling it uniformly.

### 4. Surface, atmosphere, and contact polish

- Complete Landscape layer logic and material scale before lighting polish.
- Integrate foundations, retaining walls, stairs, drainage, paths, banks, roots, debris, dampness, moss, and erosion where physically plausible.
- Build lighting as a coherent system of sun, sky, clouds or weather, atmosphere, fog, exposure, and post process.
- Change one major look-development variable at a time and compare from fixed cameras.

Lighting and scatter cannot compensate for weak terrain, insufficient assets, poor contact, or a flat composition.

## Validate and iterate by cause

1. Capture the required evidence in [quality-gates.md](references/quality-gates.md).
2. Ask the independent supervisor for the applicable target or full-level verdict when delegation is available.
3. Score each category. A single hard failure blocks acceptance even when the average is high.
4. Name the weakest system and repair it before adding more decoration.
5. Compare baseline, change, and result from the same camera. Keep changes only when they improve the target without damaging another required view or gameplay.
6. In PIE, verify spawn, traversal, capsule clearance, collision, stairs, banks, water edges, boundaries, and representative sightlines.
7. Inspect performance, streaming, LOD or instancing, runtime warnings, and persistence.
8. Save affected levels and owned assets after successful gates.
9. Record transferable lessons and failed approaches in the iteration log. Keep project paths, actor names, exact coordinates, and asset-pack anecdotes out of the reusable skill.

## Preserve reusable production assets

When a visual system receives independent approval, separate its portable logic
from project-specific content. Catalog the source, dependencies, evidence,
approval scope, required substitutions, and `REVALIDATION_REQUIRED` state.

Use `scripts/install_production_asset_templates.py --project-root <root>` to
install the plugin's dependency-free catalog and system-contract templates into
a project. Refuse overwrites by default. Never distribute third-party meshes,
textures, materials, or derived Unreal packages unless their license explicitly
permits redistribution.

Keep exact approved UAssets in a project-owned read-only source library. Share
dependency-free system contracts through this plugin. Package actual UAssets
for other users only as a separately versioned Unreal content plugin after a
license and dependency audit.

## Definition of done

The golden slice and complete level meet the visual threshold; no placeholder or hard failure remains; every reachable direction has intentional foreground, midground, and background; terrain, architecture, materials, vegetation, water, and lighting read as one environment; buildings sit on verified pads or authored foundations; collision preserves the intended visual composition; routes play correctly; reserve terrain does not expose a world void; performance is viable; changes are saved; and reusable lessons are recorded.
