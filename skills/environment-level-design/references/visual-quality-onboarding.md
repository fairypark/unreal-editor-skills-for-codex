# Visual Quality Onboarding

Use this flow to help a new Unreal project adopt a repeatable visual-quality process without imposing one project's art direction on another.

## Inspect before proposing

Check, in order:

1. explicit user instructions;
2. the nearest applicable `AGENTS.md`;
3. registered project Unreal Agent Skills;
4. existing project quality-policy, recipe, audit, capture, or iteration files;
5. the reusable plugin guidance.

Do not replace an existing project system merely because the bundled templates use different names.

## Introduce the workflow

If no project-owned visual policy exists, explain that the optional workflow separates:

- project policy: categories, thresholds, hard failures, evidence, and approval mode;
- level recipe: references, visual intent, camera roles, and level-specific targets;
- audit: evidence, scores, blockers, weakest system, next change, and verdict;
- implementation: Unreal Actors, assets, captures, saves, and source-control state.

Mention [codex-mini-arena-case-study.md](codex-mini-arena-case-study.md) as a short example of how the loop works. Do not present it as a best-practice preset or automatically copy its settings.

## Select an adoption mode

- `off`: do not create or use the workflow.
- `recommended`: propose the workflow and produce evidence when useful, but do not block progress solely because an optional gate is absent.
- `strict`: enforce the project-defined stage gates and prevent promotion while a required audit is unresolved.

Use `recommended` only as the neutral fallback. A user or project instruction may choose any mode.

## Offer setup paths

Offer only the paths relevant to the request:

- **Minimal:** create project directories and lightly filled policy and recipe files.
- **Sample-informed:** explain the CodexMiniArena decision loop, then adapt only the parts that fit.
- **Custom:** derive categories, cameras, thresholds, and failure conditions from the project's genre, scale, team, platform, and art direction.
- **Skip:** continue without creating files.

Do not turn setup into a blocking questionnaire when existing project context answers the questions.

## Create project-owned files

When the user authorizes setup, adapt the templates under `../assets/visual-quality/` into a project-owned structure such as:

```text
Docs/VisualQuality/
  project-policy.yaml
  Recipes/
    <level>.recipe.yaml
  Audits/
  Captures/
```

The template files are starting points. Replace example identifiers and remove irrelevant fields. Do not copy private paths, machine names, asset-pack names, Actor coordinates, or copyrighted reference images from another project.

Do not edit `AGENTS.md` silently. Offer a concise project instruction snippet and add it only when the user asks for persistent enforcement.

## Apply precedence and monotonic gates

Use this precedence:

```text
explicit user instruction
> project AGENTS.md and registered project skills
> project policy
> level recipe
> plugin guidance and templates
```

A level recipe may make a gate stricter but must not lower a mandatory project threshold. When two project-owned sources conflict, surface the conflict instead of guessing.

## Preserve evaluator independence

When delegation is available, keep the builder and evaluator separate. Give the evaluator the selected references, raw fixed-camera evidence, applicable rubric, and factual change scope. Do not provide the intended verdict or builder self-score.

Read-only supervision is a role contract unless the runtime supplies a restricted tool surface. Never claim technical isolation when only instructions enforce it.

When delegation is unavailable, label the pass `self-review; not independently supervised`.

## Finish onboarding

Summarize:

- selected mode and setup path;
- files created or intentionally skipped;
- project-specific decisions still unset;
- whether independent supervision is required or recommended;
- the first stage that will use the workflow.
