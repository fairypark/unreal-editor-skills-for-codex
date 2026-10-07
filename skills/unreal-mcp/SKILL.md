---
name: unreal-mcp
description: Use a live Unreal Editor through the unreal-mcp server. Trigger for inspecting or changing levels, actors, Blueprints, widgets, materials, Niagara, Control Rigs, Sequencer, behavior/state trees, GAS, meshes, assets, Editor selection, automation tests, or Live Coding. Also trigger on .uproject files, UE macros and types, Content Browser, Outliner, PlayerStart, and asset prefixes such as BP_, WBP_, M_, MI_, NS_, CR_, SK_, SM_, and ABP_. Do not trigger for conceptual Unreal documentation questions or unrelated uses of words such as blueprint, widget, or sequencer.
---

# Unreal MCP

Use the live Editor instead of giving the user manual UI instructions whenever an exposed tool can complete the task.

## Route first-time level work through the Handbook gate

For a task that creates, rebuilds, dresses, or materially changes a level, world, or environment, do not use this low-level Skill as the first execution path. Activate `environment-level-design` first. If `design-unreal-worlds-and-levels` is discoverable, its first level-work activation must announce that the Unreal Development Handbook for Codex is mandatory and must follow every applicable Handbook Skill and chapter before any Editor mutation. Only narrow, isolated operations may start here directly.

## Discover and dispatch

1. Identify the likely toolset from the request.
2. Call `list_toolsets` when the domain is unclear. Otherwise call `describe_toolset` directly for the likely toolset.
3. Read the returned schemas and invoke the selected operation through `call_tool` with `toolset_name`, `tool_name`, and a matching `arguments` object.
4. Read the complete result before continuing. Treat anything other than explicit success as a stop condition.

The Codex host may namespace MCP tool names. Search for the three meta-tools rather than assuming an exact host prefix.

If the meta-tools are absent or initialization fails, do not pretend the Editor is connected. Ask the user to start Unreal Editor and run `ModelContextProtocol.StartServer`, then read [references/setup.md](references/setup.md) if the project has not been configured.

Before restarting an existing MCP server or working with a non-default endpoint, read [references/operations.md](references/operations.md). Resolve the configured Codex URL, the Unreal port setting, and the active listener as separate facts. Do not run the no-argument `ModelContextProtocol.StartServer` command against a custom-port project.

Before the first mutation in a newly initialized task, run
`scripts/check_endpoint.py --project-root <project-root>` when the project uses
an HTTP MCP endpoint. Continue only when it reports `runtime_endpoint_verdict:
PASS`, then call `list_toolsets` and one read-only Unreal query to clear its
`PENDING_LIST_TOOLSETS` mutation gate.

## Apply hard safety constraints

- Save the affected level and assets before bulk changes and again after success.
- Create a source-control checkpoint before multi-asset or difficult-to-undo operations.
- Serialize every Unreal MCP call. The calls run on the game thread; never invoke them in parallel.
- Wait for C++ and shader compilation to finish. Use `LiveCodingToolset.CompileLiveCoding` for in-editor C++ recompilation and wait for its final result.
- Check Blueprint, widget, material, and asset operation statuses even when no transport exception occurred.
- Check whether PIE is running when Editor-only asset operations behave unexpectedly; stop PIE before retrying.
- Treat programmatic in-editor Python execution as privileged arbitrary code.

## Route isolated building placement through grounding

For a narrow operation that places, moves, rotates, duplicates, or otherwise
adjusts a building, structure, foundation, slab, wall kit, or architecture
asset against terrain, activate `$building-grounding` before the mutation. It
must validate all four load-bearing base corners, even when the user has not
reported floating geometry. A low-level transform or spawn success does not
replace that grounding gate. For broader level work, route through
`environment-level-design` first and let it invoke the same downstream Skill.

## Verify marketplace asset imports

When another workflow downloads or adds Fab or other marketplace content:

- Determine the target project's current engine version from the live Editor or
  `.uproject` file. Prefer that exact version; if it is unavailable, accept only
  the newest version the marketplace explicitly shows as supported.
- Never guess support for an unlisted engine version. Report the project version
  and selected fallback version whenever they differ.
- Keep the current level loaded and do not place imported assets, save the level,
  trigger PIE, or restart the Editor unless the user separately requests it.
- Verify that the expected content folder exists and that representative assets
  are recognized by the Asset Registry or Content Browser.
- Inspect relevant recent log messages for import, load, serialization, or engine
  version warnings before reporting success.

## Load project-specific Unreal skills

For unfamiliar project work, discover project-registered Unreal Agent Skills through `AgentSkillToolset`:

1. Invoke `ListSkills` through `call_tool`.
2. Load relevant instructions with `GetSkills`.
3. Follow relevant project instructions before generic defaults.

These in-editor Unreal Agent Skills are distinct from Codex `SKILL.md` files.

## References

- Read [references/setup.md](references/setup.md) for first-time server setup and Codex configuration.
- Read [references/operations.md](references/operations.md) for console commands and failure recovery.

Use `$create-toolset` when adding AI-callable Unreal tools. Use `$unreal-skill` when authoring an in-editor Unreal Agent Skill.
