# Unreal Editor Skills for Codex

Community-maintained Codex workflows for controlling and extending a live Unreal Editor through MCP.

This project adapts Epic Games' MIT-licensed `unreal-engine-skills-for-claude-code-plugin` for Codex. It contains Codex skills, MCP wiring, and a Windows-native project-context hook. It does not bundle Unreal Engine code, `ModelContextProtocol`, or `AllToolsets`.

## Install

Add the Fairypark marketplace and install the plugin:

```powershell
codex plugin marketplace add fairypark/unreal-editor-skills-for-codex
codex plugin add unreal-editor-skills-for-codex@fairypark
```

Fully quit and restart the Codex or ChatGPT desktop app after installation. Start a new Codex task in the Unreal project so the installed skills, MCP connection, and session hook are loaded.

To update an existing installation:

```powershell
codex plugin marketplace upgrade fairypark
codex plugin add unreal-editor-skills-for-codex@fairypark
```

## Included skills

- `unreal-mcp`: inspect and mutate a live Unreal Editor safely.
- `create-toolset`: author AI-callable Unreal C++ or Python toolsets.
- `unreal-skill`: create project- or plugin-specific Unreal Agent Skills.
- `environment-level-design`: design, build, and iteratively validate production-quality
  environment levels from concept art through Landscape, ecology, gameplay, collision, and
  360-degree visual QA. When agent delegation is available, it assigns a separate read-only
  visual supervisor for golden-slice, target-repair, and full-level acceptance gates. When
  the companion `UnrealToolsetsExtension` is available, persistent `CameraActor` evidence can
  be written as a verified PNG plus evidence receipt and revalidated immediately before
  independent-supervisor handoff.
- `unreal-usage-metrics`: manage optional local-only usefulness metrics.

## Optional local usage metrics

The plugin can collect small operational signals to help evaluate whether its Unreal
workflows are reliable and useful. Collection is off until the user explicitly opts in.
The first-use question appears only in an Unreal project and does not delay the current task.

Metrics remain on the user's device. The plugin never stores prompts, assistant messages,
paths, project names, Actor or Asset names, tool arguments, tool response contents, or raw
session identifiers. Events are retained for up to 90 days and can be summarized or deleted
at any time.

Ask Codex naturally:

- `Enable Unreal plugin usage metrics.`
- `Disable Unreal plugin usage metrics.`
- `Show my Unreal plugin usage metrics summary.`
- `Show my UnrealToolsetsExtension usefulness summary.`
- `Show a shareable UnrealToolsetsExtension usefulness summary.`
- `Rate UnrealToolsetsExtension usefulness 5 out of 5.`
- `Delete the stored Unreal plugin usage metrics.`

Disabling stops new collection but preserves existing events. Deletion is a separate explicit
action. See [`docs/USAGE_METRICS.md`](docs/USAGE_METRICS.md) for the complete privacy and
maintenance contract.

## Prerequisites

1. An Unreal Engine build that includes the `ModelContextProtocol` and `AllToolsets` plugins.
2. Both plugins enabled in the target `.uproject`.
3. Unreal Editor running with the server started:

   ```text
   ModelContextProtocol.StartServer
   ```

The bundled MCP connection uses Unreal's default endpoint, `http://127.0.0.1:8000/mcp`.

If the local environment requires a custom endpoint, configure it as a project-scoped override and keep the Unreal server endpoint and the effective Codex MCP URL in sync.

## Verify

1. Start Unreal Editor and its MCP server.
2. Start a new Codex task in the Unreal project.
3. Ask: `List the actors in the current level.`
4. Confirm that Codex discovers the Unreal toolsets and returns live Editor state.

The workflow was live-tested with Unreal Engine 5.8: MCP initialization, all three meta-tools, toolset discovery, project Agent Skill discovery, current-level lookup, and a read-only actor query completed successfully. The published default remains Unreal's port `8000`.

For environment work, ask Codex to build or improve a level. The environment skill keeps the
primary agent as the builder and uses a separate visual supervisor when the runtime supports agent
delegation. When supported, the supervisor runs as `gpt-5.6-sol` with `xhigh` reasoning while the
builder keeps its own independent reasoning setting. The supervisor receives raw fixed-camera
evidence and remains read-only; without
delegation, the same pass is explicitly labeled as a non-independent self-review. Evidence
promotion requires a persistent camera, a unique local PNG, its paired `.evidence.json`
receipt, and successful handoff-time verification rather than the existence of a screenshot
filename alone.

## Safety

MCP tools can modify live `UObject` state, assets, levels, and project files. Save and create a source-control recovery point before bulk operations. Keep Unreal MCP calls sequential, verify every result, and treat programmatic in-editor Python execution as privileged.

## Attribution

See `LICENSE` and `THIRD_PARTY_NOTICES.md`. This project is not affiliated with or endorsed by Epic Games, OpenAI, or Anthropic.

Reusable English and Korean introduction copy is available in
[`docs/PLUGIN_DESCRIPTION.md`](docs/PLUGIN_DESCRIPTION.md).
