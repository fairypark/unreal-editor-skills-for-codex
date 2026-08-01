# Visual Quality Workspace Onboarding

Use this flow only to install or integrate the bundled project-file templates. Obtain categories, thresholds, required cameras, and approval policy from the project or from `validate-unreal-production` when the Handbook plugin is installed.

## Inspect existing project state

Check explicit user instructions, applicable `AGENTS.md`, registered Unreal Agent Skills, and existing policy, recipe, audit, capture, or iteration files. Do not replace a project-owned system because the bundled templates use different names.

## Select an execution mode

- `off`: create nothing.
- `recommended`: offer project files and evidence capture without making their absence a blocker.
- `strict`: enforce the project-defined gates and keep promotion pending while required evidence is unresolved.

Use `recommended` only as a fallback when neither the user nor project policy chooses a mode.

## Create project-owned files

When authorized, adapt the files under `../assets/visual-quality/` into a structure such as:

```text
Docs/VisualQuality/
  project-policy.yaml
  Recipes/
    <level>.recipe.yaml
  Audits/
  Captures/
```

Replace sample identifiers and remove irrelevant fields. Do not copy private paths, machine names, asset-pack names, Actor coordinates, credentials, or copyrighted reference images. Do not edit `AGENTS.md` unless the user asks for persistent project guidance.

If a project initializer is available, validate the recipe first, refuse overwrites, and require the initial state `PENDING_RUNTIME`. An initializer may create directories, overlays, empty audit structure, and pending camera entries; it must not invent captures, hashes, transforms, scores, or a passing verdict.

## Apply precedence

Use this order:

```text
explicit user instruction
> project AGENTS.md and registered project skills
> project policy
> level recipe
> plugin templates
```

Surface conflicts between project-owned sources. A local recipe may make a gate stricter but must not silently lower a mandatory project threshold.

## Report the result

List the selected mode, exact files created or skipped, unresolved project decisions, required runtime evidence, and the first stage that will use the workspace. File creation is setup, not visual approval.
