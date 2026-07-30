# CodexMiniArena Procedural Case Study

This case study demonstrates a decision loop used in one Unreal environment project. It is not a preset, a universal rubric, or a source of default thresholds.

## Why the project used it

The builder could produce technically complete levels that still failed the chosen visual reference. The project therefore separated implementation from stage approval and preserved decisions outside chat history.

## Procedure

1. Prepare multiple concept views covering arrival, hero, route, and reverse directions.
2. Select one primary quality reference and record prohibited failure imagery.
3. Store visual intent, fixed camera roles, and project-specific gates in a machine-readable Visual Recipe.
4. Build a small representative golden slice before broad dressing.
5. Capture clean evidence from persistent cameras without changing the comparison pose.
6. Give the recipe, reference, and raw evidence to a separate read-only evaluator.
7. If the evaluator returns `NO-GO`, repair the weakest visible system rather than adding unrelated decoration.
8. Recapture the same cameras and request another independent verdict.
9. Expand only the systems that passed their applicable gate.

## Example judgment

```yaml
verdict: NO-GO
weakest_system: background_enclosure
visible_reason: reverse view exposes an unfinished environment boundary
next_change: repair midground enclosure without changing the camera
lesson: a strong hero view cannot compensate for a failing reverse view
```

This example shows the output shape and reasoning discipline. It does not prescribe the project's categories, score floor, camera count, slice dimensions, collision policy, or art direction.

## Transferable lessons

- Use a persistent camera to preserve comparison integrity.
- Treat a focused target pass and full-level approval as separate decisions.
- Preserve failed audits; they explain why the next change exists.
- Repair the weakest system before increasing scale or density.
- Keep project-specific settings in project files, not in the reusable plugin.
- Describe instruction-only read-only supervision honestly; it is not a technical permission boundary.

## What is intentionally omitted

- project and machine paths;
- Actor transforms and asset identifiers;
- proprietary or licensed reference images;
- full recipes and production audits;
- project-specific PCG, lighting, collision, and performance settings.
