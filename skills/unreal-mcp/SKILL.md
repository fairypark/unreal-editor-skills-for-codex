---
name: unreal-mcp
description: Use a live Unreal Editor through the unreal-mcp server. Trigger for inspecting or changing levels, actors, Blueprints, widgets, materials, Niagara, Control Rigs, Sequencer, behavior/state trees, GAS, meshes, assets, Editor selection, automation tests, or Live Coding. Also trigger on .uproject files, UE macros and types, Content Browser, Outliner, PlayerStart, and asset prefixes such as BP_, WBP_, M_, MI_, NS_, CR_, SK_, SM_, and ABP_. Do not trigger for conceptual Unreal documentation questions or unrelated uses of words such as blueprint, widget, or sequencer.
---

# Unreal MCP

Use the live Editor instead of giving the user manual UI instructions whenever an exposed tool can complete the task.

## Discover and dispatch

1. Identify the likely toolset from the request.
2. Call `list_toolsets` when the domain is unclear. Otherwise call `describe_toolset` directly for the likely toolset.
3. Read the returned schemas and invoke the selected operation through `call_tool` with `toolset_name`, `tool_name`, and a matching `arguments` object.
4. Read the complete result before continuing. Treat anything other than explicit success as a stop condition.

The Codex host may namespace MCP tool names. Search for the three meta-tools rather than assuming an exact host prefix.

If the meta-tools are absent or initialization fails, do not pretend the Editor is connected. Ask the user to start Unreal Editor and run `ModelContextProtocol.StartServer`, then read [references/setup.md](references/setup.md) if the project has not been configured.

## Apply hard safety constraints

- Save the affected level and assets before bulk changes and again after success.
- Create a source-control checkpoint before multi-asset or difficult-to-undo operations.
- Serialize every Unreal MCP call. The calls run on the game thread; never invoke them in parallel.
- Wait for C++ and shader compilation to finish. Use `LiveCodingToolset.CompileLiveCoding` for in-editor C++ recompilation and wait for its final result.
- Check Blueprint, widget, material, and asset operation statuses even when no transport exception occurred.
- Check whether PIE is running when Editor-only asset operations behave unexpectedly; stop PIE before retrying.
- Treat programmatic in-editor Python execution as privileged arbitrary code.

## Load project-specific Unreal skills

For unfamiliar project work, discover project-registered Unreal Agent Skills through `AgentSkillToolset`:

1. Invoke `ListSkills` through `call_tool`.
2. Load relevant instructions with `GetSkills`.
3. Follow relevant project instructions before generic defaults.

These in-editor Unreal Agent Skills are distinct from Codex `SKILL.md` files.

## Handle missing structured tools

- Do not present a Slate workflow, generic property mutation, or programmatic Python execution as equivalent to a missing domain API.
- For Landscape creation, heightmap or weightmap import, reimport, material assignment, height statistics, building-pad validation, or save requests, inspect official toolsets and any third-party extension actually returned by `list_toolsets`. Prefer an official typed operation when it fully satisfies the request. Never assume `LandscapeExtensionToolset` is installed. If no discovered structured tool covers the operation, report the runtime capability gap and use `$create-toolset` with its Landscape reference to update the external-project handoff contract.
- Use Slate UI automation only for a user-approved, immediate workaround after confirming that no structured tool can perform the operation. Save before the action, keep the observed subtree minimal, and call `SlateInspectorToolset.Unobserve` in a finally-style cleanup immediately after the UI action. Verify the resulting Landscape with structured reads; UI feedback alone is not proof of success.

## References

- Read [references/setup.md](references/setup.md) for first-time server setup and Codex configuration.
- Read [references/operations.md](references/operations.md) for console commands and failure recovery.

Use `$create-toolset` when adding AI-callable Unreal tools. Use `$unreal-skill` when authoring an in-editor Unreal Agent Skill.
