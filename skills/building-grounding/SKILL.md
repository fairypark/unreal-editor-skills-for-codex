---
name: building-grounding
description: Place or repair building Actors on sloped Landscape terrain by sampling all four load-bearing base corners, fitting a support plane, preserving the intended footprint and scale, and verifying contact at every corner. Use when a building floats, sinks, tilts, or spans uneven terrain; do not treat a center trace or a three-corner match as success.
---

# Four-Corner Building Grounding

Use this Skill for a narrow building-placement or grounding operation in a live
Unreal Editor. It is an execution contract for a single building or a small,
explicit batch. For broad level dressing or a new site, activate
`environment-level-design` first and follow its Handbook and stage gates.

## Define the postcondition

Before mutating the level, state:

- the target Actor or building assembly and the current level;
- the load-bearing footprint to use (the actual foundation/base, not decorative
  overhangs, foliage, or an arbitrary Actor AABB);
- the grounding mode: `SLOPE_ALIGN` when the building may tilt with a planar
  slope, or `VERTICAL_FOUNDATION` when walls, gameplay, or a kit rule require
  the building to remain upright;
- the project's contact tolerance and allowable penetration, or the documented
  default if the project has none;
- the recovery point and the evidence needed to prove the result.

The success condition is per-corner, not an average: all four named base
corners must have a trusted terrain hit and a final signed contact residual
within tolerance. A result with three grounded corners, a good center height,
or a low average error is `FAIL`.

## Inspect before placement

1. Confirm the `.uproject`, open world, target selection, construction
   provenance, and whether the target is a single rigid Actor or a parented
   assembly. Save or establish a source-control/saved-copy recovery point
   before a difficult-to-undo placement.
2. Read the complete transform and preserve the intended location, heading,
   and scale as separate inputs. Inspect the final-scale mesh/components,
   pivot, local bounds, collision, Nanite/LOD behavior, and any existing
   foundation component. Do not edit a shared source mesh to solve one level's
   contact problem.
3. Derive four local support points from the load-bearing base plane. For a
   rectangular footprint, use the local min/max X and Y at the actual base Z
   and label the points consistently (`SW`, `SE`, `NW`, `NE`) relative to the
   building's intended heading. If the footprint is irregular or the mesh
   pivot is ambiguous, use an explicit foundation/support component or stop
   and request one; do not silently substitute a visual bounding box.

## Sample the authoritative surface

Sample the terrain at all four points after applying the intended horizontal
placement and current scale. Use long downward queries from above the
building's bounds and ignore the target Actor and its children. The hit must be
from the trusted Landscape or explicitly approved terrain provider; reject
hits on props, volumes, temporary collision, or the building itself. Preserve
the corner label, world query point, hit position, hit normal, hit Actor/class,
and query status for every sample.

Also sample the footprint center and four edge midpoints as diagnostics. They
help find a ridge, ditch, or collision anomaly, but they never replace the four
corner acceptance checks. If any required corner has no authoritative hit,
stop with `PENDING_EVIDENCE` and do not claim that the building is grounded.

## Solve the placement

### `SLOPE_ALIGN`

Use this mode only when the building is allowed to follow the slope.

1. Fit a support plane to the four terrain hit positions. Use the plane normal
   to solve roll and pitch while preserving the intended heading as the
   projection of the building's forward direction onto that plane. Preserve
   scale and avoid an arbitrary yaw change.
2. Solve the translation from the chosen footprint anchor so the transformed
   base plane lies on the fitted support plane. Recompute all four transformed
   corners after the rotation and translation; do not rely on the pre-rotation
   trace results.
3. If the fourth point or edge diagnostics has a residual over tolerance, the
   terrain is not sufficiently planar for a rigid placement. Do not keep
   rotating until one corner is buried. Switch to `VERTICAL_FOUNDATION`, an
   authored stepped/retaining foundation, or a bounded site-grade operation
   allowed by the design contract.

### `VERTICAL_FOUNDATION`

Keep the building's world-up relationship and intended yaw. Create or adjust a
level-local plinth, slab, piers, retaining edge, or graded building pad under
the explicit footprint so each of the four support corners has a real contact
surface. Keep that support owned by the level or project variant; do not alter
the shared building mesh. Re-sample the support and Landscape separately, and
verify that the foundation does not create an unexpected collision, navigation
blocker, or visible gap around the perimeter.

If the project explicitly permits controlled burial, the chosen support plane
may remove positive gaps with only the configured penetration epsilon. Record
that exception and verify collision; burial is not a substitute for a
foundation when it exposes a wall, doorway, or navigable edge.

## Apply bounded mutations

- Make one placement/foundation batch at a time, with explicit targets.
- Keep Unreal game-thread calls sequential and inspect the returned status and
  warnings before the next call.
- Preserve location, rotation, and scale together; never overwrite the full
  transform with a partial default.
- For a parented assembly, place the parent or the authored support system and
  then re-read representative children. Do not independently drift four
  children to fake a rigid building's grounding.
- After a timeout or ambiguous result, inspect the current Actor and child
  state before retrying so duplicate foundations or placements are not created.

## Verify the four-corner result

After every mutation batch:

1. Re-read the final transform, bounds, support components, and save state.
2. Recompute the four final world-space support corners and query the trusted
   terrain/support surface again. For each of `SW`, `SE`, `NW`, and `NE`, record
   the hit source, signed gap or penetration, surface normal, and pass/fail
   against the configured tolerance.
3. Require all four rows to pass. Check the center and edge midpoints for
   obvious terrain intersections or unsupported spans, then inspect a contact
   view from at least two sides when visual evidence is required.
4. Run the relevant collision and Navigation check, and a short PIE check when
   the building changes a route, doorway, physics interaction, or walkable
   surface. Save the affected level and owned foundation assets only after the
   postconditions pass, then re-read them to confirm persistence.

Report the original and final transform, the grounding mode, the four corner
  measurements, the maximum residual, surface authority, foundation/grade
  action, warnings, evidence paths, and unresolved limitations. Mark the
  result `PASS` only when all four corners are within tolerance and the saved
  state persists. Otherwise report `FAIL` or `PENDING_EVIDENCE` truthfully.
