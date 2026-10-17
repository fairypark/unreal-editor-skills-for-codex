# Vegetation sources and connected ground surfaces

Use this reference when repeated vegetation defects need source diagnosis, or when a concept calls for coherent substrate and vegetation coverage. It refines the existing source and representative-slice checks; it does not add a universal approval stage. For the paired user-review summary, see [environment-reuse-review.ko.md](environment-reuse-review.ko.md).

## Separate source, surface, and scene findings

1. Identify the exact mesh, material and instance overrides, intended role, saved version, scale range, and viewing distances. Preserve originals and use task-owned copies for changes.
2. Inspect an isolated source at the intended scale extremes and a representative scale. Cover the visible front, reverse, sides, top or underside, and a grazing player view as applicable. Do not mandate six views for an asset whose role cannot expose them; record the coverage rationale.
3. Inspect the saved asset, not only the construction buffer. Check silhouette, actual footprint, width, curvature, material slots, normals/tangents, and reverse surfaces. Recomputing normals during asset creation can replace authored normals. Open-backed scans need a backed role or a different source.
4. Record shape and surface findings separately. Examine leaf backs, dark bands, excessive transmission, clipped or fluorescent color, normal response, and mismatch with the substrate under the frozen scene lighting. A two-sided-normal adjustment is a diagnostic candidate, not an instruction to alter every foliage shader.
5. Test a small, recorded set of existing scene positions before converting the slice. Preserve the baseline source mapping and transforms for rollback. Keep the canary size proportional to the failure; 36 positions was one case, not a default.
6. If only material inputs change, reuse unchanged shape evidence and recapture the affected canary and scene views. If geometry, scale, pivot, WPO, or source mesh changes, recompute the final footprint and recheck contacts and exclusions. Do not use count equality as a substitute for transform or dependency comparison.
7. Expand only under the current slice authority. Record `shape`, `surface`, and `in_context` results with their own candidate versions and evidence in [environment-source-check.template.json](../assets/production-assets/environment-source-check.template.json). Source acceptance does not approve broad placement, wind, performance, or a new context.

Ordinary source inspection does not require custom geometry. Existing cards, meshes, and scans remain suitable when they pass the intended role and budget. Retain failed sources with their rejection reason so they are not rediscovered as approved candidates.

## Connect substrate and placement

Use [meadow-ground-cover.system.json](../assets/production-assets/meadow-ground-cover.system.json) as a dependency-free contract. Supply project-owned or licensed sources; the template contains no mesh, texture, or UAsset.

- Publish one field identity and revision with coordinate frame, units, origin policy, seed or immutable samples, extent, and authored accents. Record separate consumer mappings for placement probability, scale or species choice, and material blending. They need not produce identical masks.
- Keep route, water, hardscape, and gameplay exclusions authoritative. Apply final transformed mesh clearance after source selection, rotation, scale, and projection. The habitat field must not fill reserved space.
- Prefer one immutable data product consumed by both paths when feasible. If an offline generator and material shader separately compute the field, compare actual values at the same predeclared positions and tolerance. Include representative interiors and relevant edges, negative coordinates, origin changes, or seams. Identical equations and seeds alone are not parity evidence.
- Export scalar samples from the actual consumers; do not fabricate GPU samples by evaluating the CPU function twice. Run `scripts/validate_spatial_field_samples.py <samples.json>`. Its `PASS_PARITY_ONLY` result covers the supplied samples only, not the provenance of a GPU readback or full-field/visual equivalence.
- In the sample JSON, provide `schema_version: 1`, `authority` with `field_id`, `revision`, `coordinate_frame`, and `units`; a finite `tolerance` between 0 and 1; `reference_samples` with unique `id`, XYZ `position`, and scalar `value` in [0,1]; and nonempty `consumers`, each with a unique `id`, matching authority fields, and samples covering exactly the reference IDs and positions. Record acquisition method and sample-coverage reasoning with the project evidence.
- Retain the parity result and compare dense colonies, bare intervals, edge transitions, ordinary repeated areas, and reverse views in the scene. A numerical pass cannot approve the image.
- For a grass/dirt blend, apply grass-specific tint to the grass branch before mixing when the intended material model requires unaffected dirt. Inspect pure grass, pure dirt, and mixed regions; confirm texture/normal scale and source-specific changes. Do not adjust global exposure to conceal a source response defect.

## Preserve source quality while changing the backend

An instancing backend failure is separate from an art failure. Before switching a failing backend, retain crash or error evidence and classify partial output. A supported alternative needs a bounded add/readback/clear canary, preserved source mappings, seeds, transforms, exclusions and collision intent, then saved-state and scene regression evidence. Do not make HISM, PCG, or any other backend a universal default based on one engine/build incident.

## Revalidation scope

Reuse evidence only while its inputs are unchanged. New source geometry reopens footprint and shape checks; new shading reopens surface and affected scene views; a changed field reopens its consumers and boundaries; broader coverage reopens repetition and composition. The project still owns independent visual approval. Scene-specific blend ratios, transmission values, normal policies, and lighting numbers stay in the scene recipe.
